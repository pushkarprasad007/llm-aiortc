import asyncio
from typing import Optional

from aiortc import MediaStreamTrack, RTCDataChannel
from aiortc.contrib.media import MediaPlayer


class PlaybackStreamTrack(MediaStreamTrack):
    kind = "audio"
    response_ready: bool = False
    previous_response_silence: bool = False
    track: MediaStreamTrack = None
    counter: int = 0
    time: float = 0.0
    audio_files = []
    step: int = 1
    last_step: int = 0
    response_ended = False
    channel: Optional[RTCDataChannel] = None
    is_silence = False

    def __init__(self):
        super().__init__()  # don't forget this!

    def reset_step(self):
        print("[reset_step] Came in reset_step")
        self.step = 1
        self.last_step = 0
        self.audio_files = []

    def increase_step(self):
        self.step += 1

    def set_last_step(self, last_step):
        print(f"[set_last_step] {last_step}")
        self.last_step = last_step

    def add_partial_audio(self, audio_wav):
        self.audio_files.append(audio_wav)

    def select_track(self):
        self.is_silence = False
        # print(f"[select_track] response_ready : {self.response_ready}")
        # print(f"[select_track] step : {self.step}")
        # print(f"[select_track] last_step : {self.last_step}")
        # print(f"[select_track] audio_files : {self.audio_files}")
        # print(f"[select_track] len(audio_files) : {len(self.audio_files)}")
        # if self.response_ready and len(self.audio_files) >= self.step and self.step <= self.last_step:
        if self.response_ready and (len(self.audio_files) >= self.step) and ((self.last_step == 0) or (self.step <= self.last_step)):
            audio_file = self.audio_files[self.step - 1]
            self.track = MediaPlayer(audio_file, format="wav", loop=False).audio
            # print(f"[select_track] Came in track for {audio_file}")
        else:
            #self.track = MediaPlayer("silence.wav", format="wav", loop=False).audio
            self.track = MediaPlayer("silent-250.wav", format="wav", loop=False).audio
            self.is_silence = True
            # print("[select_track] Came in silence")
        if self.channel is not None and self.channel.readyState == "open":
            if self.response_ready:
                self.channel.send("playing: response")
                self.previous_response_silence = False
            else:
                if not self.previous_response_silence:
                    self.channel.send("playing: silence")
                    self.previous_response_silence = True

    async def recv(self):
        self.counter += 1
        if self.track is None:
            self.select_track()
        try:
            async with asyncio.timeout(1):
                frame = await self.track.recv()
        except Exception as e:
            # print("[recv] Came in Exception")
            # Check if this was a silence track or otherwise
            # If not silence, means a LLM partial audio track has finished
            if self.is_silence == False:
                print(f"[recv] Came inside step {self.step}")
                # Increase the step of the track
                self.increase_step()
                # If the current step is highest 
                if self.last_step > 0 and self.step > self.last_step:
                    self.reset_step()
                    # print("[recv] Came inside last step")
                    self.response_ready = False
            self.select_track()
            frame = await self.track.recv()
        if frame.pts < frame.sample_rate * self.time:
            frame.pts = frame.sample_rate * self.time
        self.time += 0.02
        return frame
