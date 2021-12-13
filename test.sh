PUBLIC_URL=$(terraform output -raw public_url)
REQUEST_ID=$(uuidgen)

echo "Request ID: $REQUEST_ID"

curl -s \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{ "file_name": "earth.blend", "request_id": "'$REQUEST_ID'" }' \
    "$PUBLIC_URL/render-job" | jq
