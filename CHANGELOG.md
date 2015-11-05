# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased][unreleased]


## [0.2.0] - 2015-11-05
### Added
- Speed up server side queries
- Added purchase price to item - issue #95
- Added currency to config for prices

### Changed
- Updated install steps in documentation
- User can not change quantity via /items endpoint - issue #102
- Items have to have one master barcode - issue #99
- Lazy creating barcodes - issue #105

### Removed
- User can not delete the master barcode - issue #99

### Fixed
- Fixed saving processes in item sidebar and view - issue #98
- Fixed some language issues - issue #91
- Item quantity can not be run under 0 - issue #93
- Count/quantity selector arrows can be bigger - issue #90


## 0.1.0 - 2015-10-08
### Added
- User login, logout
- Manage items and its barcodes, units, vendors
- Add/remove items in store
- Able to use barcode reader for collecting items
- Can use barcode printer to create labels


[unreleased]: https://github.com/andras-tim/StoreKeeper/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/andras-tim/callrecord-renamer/compare/v1.0.0...v0.2.0
