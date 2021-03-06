# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased][unreleased]


## [0.5.0] - 2016-03-18
### Changed
- Updated server and client dependencies to the latest version:

    New system dependencies:

    - `libjpeg-dev`
    - `libffi-dev`
    - `zlib1g-dev`
    
- Customizable search for item types. Now, the item selector will return items only - issue #119

### Fixed
- Table footer border and alignment on Items view
- Turned off autocomplete when it is not necessary or annoying - issue #139
- Persistent storage is thread-safe now - issue #137
- Separated production and test persistent storage - issue #111
- Small performance improvements and responsive fixes in WebUI
- Fixed login issue in Firefox
- Fixed number input of pager in Firefox
- Moved dropdown-menu elements to body to avoid cropping by the parent container - issue #147
- Fixed item selection problem in typeaheads - issue #100
- Removed annoying warning about bad value from quantity input fields
- Fixed commit-able state check of Item sideber - issue #141


## [0.4.0] - 2016-02-29
### Added
- Added location filed to Item
- Warning for low item quantity on UI - issue #2

### Changed
- Moved common email related settings from "Log" to "Email" in config file

### Fixed
- Turn off properly browser autocomplete in typeaheads too - issue #132


## [0.3.0] - 2016-01-07
### Added
- Configurable log and message format
- Start logging changes (without api export and WebUI currently) - issue #128

### Changed
- Replaced database migration framework - issue #115

    (please, follow the [custom upgrade process](http://storekeeper.readthedocs.org/en/v0.3.0/upgrade.html#upgrade-from-v0-2-1-to-v0-3-0))

### Fixed
- Sometimes left tooltips - issue #86
- Fetching Items once on pageload
- Can not logging errors via email when message contains UTF-8 characters - issue #126


## [0.2.1] - 2015-11-09
### Added
- Item list updates automatically - issue #92
- Logging the printer jobs - issue #121

### Changed
- Order item finder downdrop by name and quantity - issue #118
- Improved input validation
- Auto scaling label title
- Abort generating labels with too wide barcodes - issue #117

### Fixed
- Do not wrap button fields - issue #122
- User can printing multiple label copies with one copy per job - issue #120
- Support long double accents on labels - issue #116


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


[unreleased]: https://github.com/andras-tim/StoreKeeper/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/andras-tim/StoreKeeper/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/andras-tim/StoreKeeper/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/andras-tim/StoreKeeper/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/andras-tim/StoreKeeper/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/andras-tim/StoreKeeper/compare/v0.1.0...v0.2.0
