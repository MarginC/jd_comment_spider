#!/bin/sh

cat jd_comment_uniq.json | sort | uniq > jd_comment_uniq.json.tmp
mv -f jd_comment_uniq.json.tmp jd_comment_uniq.json
