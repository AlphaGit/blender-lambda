curl -s \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{ "file_name": "earth.blend", "frame_start": 1, "frame_end": 2 }' \
    "$(terraform output -raw public_url)/render-job" | jq
