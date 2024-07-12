from asyncio import Task
import io
import numpy as np
import uuid
import os
from pydub import AudioSegment
import numpy as np
from aiortc import RTCPeerConnection, RTCDataChannel, MediaStreamTrack
from av import AudioFrame

from playback_stream_track import PlaybackStreamTrack
import logging


class State:
    track: MediaStreamTrack
    buffer: list = []
    recording: bool = False
    task: Task
    sample_rate: int = 16000
    counter: int = 0
    response_player: PlaybackStreamTrack = None

    logger = logging.getLogger("pc")

    def __init__(self):
        self.pc = RTCPeerConnection()
        self.id = str(uuid.uuid4())
        self.response_player = PlaybackStreamTrack()
        self.filename = f"{self.id}.wav"
        print(self.pc)
        print(self.id)
        print(f"Counter : {self.response_player.counter}")

    def log_info(self, msg, *args):
        self.logger.info(self.id + " " + msg, *args)

    def append_frame(self, frame: AudioFrame):
        buffer = frame.to_ndarray().flatten().astype(np.int16)
        # check for silence
        max_abs = np.max(np.abs(buffer))
        if True or max_abs > 50:
            if self.sample_rate != frame.sample_rate * 2:
                self.sample_rate = frame.sample_rate * 2
            self.buffer.append(buffer)

    def flush_audio(self):
        self.buffer = np.array(self.buffer).flatten()
        self.log_info(f"Buffer Size: {len(self.buffer)}")

        print("Came in flush_audio")
        # Convert to mp3
        audio = AudioSegment(
            self.buffer.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=self.buffer.dtype.itemsize,
            channels=1
        )
    
        print("Came in flush_audio - before export to mp3")
        # Save to file
        output_filename = 'user.mp3'
        audio.export(output_filename, format="mp3")
    
        # # Also prepare data to return
        # buffer = io.BytesIO()
        # audio.export(buffer, format="mp3")
        # mp3_data = buffer.getvalue()
        # print("Came in flush_audio - Returning")
    
        # self.log_info(f"MP3 file saved as: {os.path.abspath(output_filename)}")
    

        return None
