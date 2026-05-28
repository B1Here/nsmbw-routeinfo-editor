# RouteInfo-Editor

[![Latest Release][release-version-image]][releases-url] ![Repo Stars][stars-image]

A simple NSMBW RouteInfo editor and CSV-generator Add-on for [Blender](https://blender.org/)

Define and generate RouteInfo CSV files for your `CS_Wxy` armatures.

Download the latest release [here](https://github.com/B1Here/routeinfo-gen/releases).

## Usage

- Point data can be edited in the Bone Properties section. Make sure you have a bone with a valid point name selected in Edit Mode.
- Routes can be edited in the Object Data Properties of an armature. They are generated automatically based on the bone hierachy of the respective `CS_Wxy` armature. To add/remove routes. A simple refresh of the list will do the trick.
- Validate your CSV data with the help of a single button click.
- Choose your file path and press the button to make the add-on generate the proper CSV files.

## Notices

The individual points and routes are defined by the order of the bones within the armature.

For more information on Points and Routes, read [this article](https://horizon.miraheze.org/wiki/World_Map_Data).

[release-version-image]: https://img.shields.io/github/v/release/B1Here/routeinfo-gen?logo=blender&logoColor=white
[releases-url]: https://github.com/B1Here/routeinfo-gen/releases
[stars-image]: https://img.shields.io/github/stars/B1Here/routeinfo-gen?style=flat&logo=github&color=yellow
