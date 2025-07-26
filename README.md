# Project-Drishti---Google-Agentic-AI-Hackathon
# This command streams a video file to a stream. Video is looped into the stream until you stop the command.

vaictl -p eventide-intel-jn8fi \
 -l us-central1 \
 -c application-cluster-0 \
 --service-endpoint visionai.googleapis.com \
send video-file to streams queue-feed-1 --file-path /home/saini_js2001/100_N25_h0_R1_high_compressed.mp4 --loop

# This command streams a video file to a stream. Video is looped into the stream until you stop the command.
vaictl -p eventide-intel-jn8fi \
         -l us-central1 \
         -c application-cluster-0 \
         --service-endpoint visionai.googleapis.com \
send video-file to streams entry-feed-1 --file-path /home/saini_js2001/100_N25_h0_R1_high_compressed.mp4 --loop


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