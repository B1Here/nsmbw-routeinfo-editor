# RouteInfo-Gen

[![Latest Release][release-version-image]][releases-url] ![Repo Stars][stars-image]

A simple NSMBW RouteInfo CSV-generator Add-on for [Blender](https://blender.org/)

Quickly generate boilerplate, NSMBW-ready RouteInfo CSV files for all `CS_Wxy` armatures.

Download the latest release [here](https://github.com/B1Here/routeinfo-gen/releases).

## Usage

1. Open the Dialog through the 3D Viewport via `Object > Generate RouteInfo CSVs`
2. Select whether only point, route or both types of files should be generated (default: Both)
3. Define where to save the files (default: same directory as the opened `.blend` file)
4. Choose a player animation all routes should have (not necessary if only points are generated; default: "Walk Grass")
5. Execute the script

## Notices

The individual points and routes are defined by the order of the bones within the armature.

If specific parts of the files need to be edited, then my [online-tool](https://b1here.github.io/route-editor) can help by allowing you to edit the CSV files in the browser directly.

[release-version-image]: https://img.shields.io/github/v/release/B1Here/routeinfo-gen?logo=blender&logoColor=white
[releases-url]: https://github.com/B1Here/routeinfo-gen/releases
[stars-image]: https://img.shields.io/github/stars/B1Here/routeinfo-gen?style=flat&logo=github&color=yellow
