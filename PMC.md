<!--
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Project Management Committee Documentation

## Release Procedure

1. Generate code signing key if you do not already have one for Apache. Refer to
http://apache.org/dev/openpgp.html#generate-key on how to generate a strong code
signing key.
2. Add your public key to the `KEYS` file at the root of the source code tree.
3. Create a new release branch, with version bumped to the next release version.
  1. `git checkout -b release/0.9.9`
  2. Replace all `0.9.9.dev0` in the code tree to `0.9.9`.
  3. `git commit -am "Prepare 0.9.9rc1"`
  4. `git tag -am "Apache PredictionIO Python SDK 0.9.9rc1" v0.9.9rc1`
4. Package a binary/source files.
  1. `python setup.py sdist bdist_wheel`
5. Generate MD5 and SHA512 checksums for the release candidates in dist directory.
  1. `gpg --print-md MD5 PredictionIO-0.9.9-py3-none-any.whl >
     PredictionIO-0.9.9-py3-none-any.whl.md5`
  2. `gpg --print-md SHA512 PredictionIO-0.9.9-py3-none-any.whl >
     PredictionIO-0.9.9-py3-none-any.whl.sha512`
  3. `gpg --print-md MD5 PredictionIO-0.9.9.tar.gz >
     PredictionIO-0.9.9.tar.gz.md5`
  4. `gpg --print-md SHA512 PredictionIO-0.9.9.tar.gz >
     PredictionIO-0.9.9.tar.gz.sha512`
6. Generate detached signature for the release candidate.
(http://apache.org/dev/release-signing.html#openpgp-ascii-detach-sig)
  1. `gpg --armor --output PredictionIO-0.9.9-py3-none-any.whl.asc
     --detach-sig PredictionIO-0.9.9-py3-none-any.whl`
  2. `gpg --armor --output PredictionIO-0.9.9.tar.gz.asc
     --detach-sig PredictionIO-0.9.9.tar.gz`
7. If you have not done so, use SVN to checkout
   https://dist.apache.org/repos/dist/dev/incubator/predictionio/sdk-python.
   This is the area for staging release candidates for voting.
  1. `svn co https://dist.apache.org/repos/dist/dev/incubator/predictionio/sdk-python`
8. Create a subdirectory at the SVN staging area. The area should have a `KEYS` file.
  1. `mkdir 0.9.9rc1`
  2. `cp PredictionIO-0.9.9* 0.9.9rc1`
9. If you have updated the `KEYS` file, also copy that to the staging area.
10. `svn commit`
13. Wait for Travis to pass build on the release branch.
14. Tag the release branch with a rc tag, e.g. `0.9.9rc1`.
15. Send out e-mail for voting on PredictionIO dev mailing list.

  ```
  Subject: [VOTE] Apache PredictionIO SDK Python 0.9.9 Release (RC1)

  This is the vote for 0.9.9 of Apache PredictionIO.

  The vote will run for at least 72 hours and will close on Apr 7th, 2017.

  The release candidate artifacts can be downloaded here:
  https://dist.apache.org/repos/dist/dev/incubator/predictionio/sdk-python/0.9.9rc1/

  Test results can be found here:
  https://travis-ci.org/apache/incubator-predictionio-sdk-python/builds/XXXXXX

  To install this python module:
  $ pip install PredictionIO-0.9.9.tar.gz
  or
  $ pip3 install PredictionIO-0.9.9-py3-none-any.whl

  The artifacts have been signed with Key : YOUR_KEY_ID

  Please vote accordingly:

  [ ] +1, accept RC as the official 0.9.9 release
  [ ] 0, neutral because...
  [ ] -1, do not accept RC as the official 0.9.9 release because...
  ```
16. Publish files to PyPI if the vote is passed.
  1. `twine upload dist/PredictionIO-0.9.9.tar.gz dist/PredictionIO-0.9.9.tar.gz.asc \
      dist/PredictionIO-0.9.9-py3-none-any.whl dist/PredictionIO-0.9.9-py3-none-any.whl.asc`
17. Create release tag
  1. `git tag -am "Apache PredictionIO Python SDK 0.9.9" v0.9.9`
18. Merge release/0.9.9 into master and develop branch
19. Bump up version in setup.py on develop branch

