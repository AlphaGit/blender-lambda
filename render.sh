BLENDER_FILE=$1
PUBLIC_URL=$(terraform output -raw public_url)

curl -s \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{ "file_name": "'$BLENDER_FILE'", "request_id": "'$REQUEST_ID'", "support_files": ["fire.mp4", "grass.jpg", "The_Earth_seen_from_Apollo_17_with_transparent_background.png"] }' \
    "$PUBLIC_URL/render-job" | jq
