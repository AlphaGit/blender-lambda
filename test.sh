PUBLIC_URL=$(terraform output -raw public_url)
REQUEST_ID=$(uuidgen)

echo "Request ID: $REQUEST_ID"

curl -s \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{ "file_name": "earth.blend", "request_id": "'$REQUEST_ID'", "frame_start": 1, "frame_end": 1, "support_files": ["fire.mp4", "grass.jpg", "The_Earth_seen_from_Apollo_17_with_transparent_background.png"] }' \
    "$PUBLIC_URL/render-job" | jq
