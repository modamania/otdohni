#!/bin/bash
if  test -d '.env'
then
    echo Destroing old environment
    rm -rf '.env'
fi

echo Creating environment
virtualenv .env

echo Install PIP inside virtual environment
./.env/bin/easy_install pip

echo Installing dependencies
./.env/bin/pip -E .env -r install ./build/pipreq.txt $*
