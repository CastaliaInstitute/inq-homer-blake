#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

check_header() {
  local file="$1"
  local expected="$2"
  local actual
  actual="$(head -n 1 "$repo_dir/$file")"
  if [[ "$actual" != "$expected" ]]; then
    printf 'Invalid header: %s\n' "$file" >&2
    exit 1
  fi
  printf 'OK %s\n' "$file"
}

check_header "assets/source/manifest.csv" \
  "epic,book,passage,creator,creator_role,work_title,date,collection_or_source_url,image_url,object_number,accessed,rights_status,local_file,credit_line,notes"
check_header "assets/generated/manifest.csv" \
  "epic,book,passage,working_title,creator,source_type,model_version,prompt_file,generated_on,reference_ids,curation_status,final_file,credit_line,notes"
check_header "design/plate-manifest.csv" \
  "plate_id,epic,book,passage,source_type,creator,creator_role,provenance_url,rights_status,caption,credit_line,final_file,width_px,height_px,color_profile,curation_status,prompt_or_source_record"
check_header "design/asset-checksums.csv" \
  "plate_id,final_file,sha256,width_px,height_px,color_profile,curation_status"
check_header "design/iliad-plate-selection.csv" \
  "book,plate_id,selection_status,approval_status,notes"

printf 'Manifest headers are valid.\n'
