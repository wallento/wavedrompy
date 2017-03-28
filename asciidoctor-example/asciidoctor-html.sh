#!/usr/bin/env bash
export PATH=$PATH:$(pwd)/..
asciidoctor -r asciidoctor-diagram example.adoc
