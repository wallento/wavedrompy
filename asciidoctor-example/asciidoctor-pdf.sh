#!/usr/bin/env bash
export PATH=$PATH:$(pwd)/..
asciidoctor-pdf -r asciidoctor-diagram example.adoc
