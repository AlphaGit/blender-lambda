curl -s "$(terraform output -raw public_url)/render-job" -X POST | jq
