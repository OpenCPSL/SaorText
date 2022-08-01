# SaorText

SaorText converts subtitle data from TV broadcasts into a human readable format.  It has been developed using the Saorview TV service in Ireland, which uses the EBU subtitle format.  

Subtitles are broadcast in a manner designed to enable a TV set to render the subtitles on screen at the correct time to correspond with the video.  The method in which this is done often results in data which is not easy for humans to read.  SaorText parses this data into a human readable transcript, which makes it straightforward to follow interviews and discussions.

SaorText has applications for historian systems, searchability of TV archives, and for machine learning.

## Extracting subtitles from TV broadcasts

Assuming that a recording of the broadcast has been made to file using MPEG-TS format, the subtitle data can be extracted using FFMPEG and the below command.  This will yield the subtitle data in Advanced SubStation Alpha format, which preserves the subtitle colour information.

`ffmpeg -txt_format ass -fix_sub_duration -i "input_file.ts" output_file.ass`
