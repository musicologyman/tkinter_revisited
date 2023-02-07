from argparse import ArgumentParser
from collections.abc import Iterable
from functools import partial
from pathlib import Path
import dataclasses
import csv

@dataclasses.dataclass
class Excerpt():
    start: float
    end: float
    label: str
    duration: float = dataclasses.field(init=False)
    
    def __post_init__(self):
        self.duration = self.end - self.start
        
def read_label_file(label_file: Path) -> Iterable[tuple[str, str, str]]:
    with label_file.open() as fp:
        return [tuple(row) for row in csv.reader(fp, dialect='excel-tab')]
    
def row_to_excerpt(row):
    start_str, end_str, label = row
    return Excerpt(float(start_str), float(end_str), label)
    
def make_ffmpeg_command(excerpt, filename=None):
    FILENAME = '"filename"'
    return f'ffmpeg -i "{filename if filename else FILENAME}" ' \
           f'-ss {excerpt.start:.3f} -t {excerpt.duration:.3f} -vcodec copy ' \
           f'-acodec copy "{excerpt.label}.mp4"'
    
def write_ffmpeg_command_file(output_file: Path, ffmpeg_commands): 
    with output_file.open(mode='w') as fp:
        for ffmpeg_command in ffmpeg_commands:
            print(ffmpeg_command, file=fp)
    
def generate_script_file(label_file: Path, media_file: Path, output_file: Path):
    rows = read_label_file(label_file)
    excerpts = [row_to_excerpt(row) for row in rows if row]
    make_ffmpeg_command_2 = \
        partial(make_ffmpeg_command, filename=media_file)

    ffmpeg_commands = [make_ffmpeg_command_2(excerpt) for excerpt in excerpts]

    write_ffmpeg_command_file(output_file, ffmpeg_commands)
    
def setup_command_line():
    parser = ArgumentParser()
    parser.add_argument('media_file', type=Path)
    parser.add_argument('label_file', type=Path)
    parser.add_argument('output_file', type=Path)
    return parser.parse_args()

def main():
    command_line_args = setup_command_line()
    rows = read_label_file(command_line_args.label_file)
    excerpts = [row_to_excerpt(row) for row in rows if row]
    make_ffmpeg_command_2 = \
        partial(make_ffmpeg_command, filename=command_line_args.media_file)

    ffmpeg_commands = [make_ffmpeg_command_2(excerpt) for excerpt in excerpts]

    output_file = command_line_args.output_file
    write_ffmpeg_command_file(output_file, ffmpeg_commands)

if __name__ == '__main__':
    main()
