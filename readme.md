# Lottie Compressor

Web app built with flask.

## Dependencies

- PNGQuant
- oxipng
- ujson

## Process

- Search for data img
- Extract
- Compress with pngquant
- Optimize with oxi png
- insert in json
- optimize json with ujson

## Usage

To start the developement server
`flask run`

To run the Pyhton compressor script only
`python3 compressor.py`

When prompted provide path to folder or file

## Todo

- [ ] Convert Button
  - [ ] Disabled on default
  - [ ] Add loading state
- [ ] Handle multiple files
  - [ ] Listing results
  - [ ] Handle upload
  - [ ] Download all
- [ ] Download
- [x] Use folders for each lottie
- [x] Create folder
- [ ] Delete folder
- [x] Show quality number
- [ ] Add Webp conversion
- [ ] Add .lottie conversion
