BLENDER_FILE=$1
shift
SUPPORT_FILES=$@

SUPPORT_FILES_STRING="[ "
for SUPPORT_FILE in $SUPPORT_FILES
do
    SUPPORT_FILES_STRING="$SUPPORT_FILES_STRING\"$SUPPORT_FILE\","
done
SUPPORT_FILES_STRING="${SUPPORT_FILES_STRING%?} ]"

PUBLIC_URL=$(terraform output -raw public_url)
DATA='{ "file_name": "'$BLENDER_FILE'", "support_files": '$SUPPORT_FILES_STRING', "frame_start": 1, "frame_end": 165 }'

curl -s \
     -X POST \
     -H "Content-Type: application/json" \
     -d "$DATA" \
     "$PUBLIC_URL/render-job"
