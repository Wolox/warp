# WARP - Seamless scaling and compression of assets for every screen density
WARP automagically enforces consistency of design, scales and greatly optimizes
the assets of your mobile project (Android and iOS).

* Consistency
Forget about maintaining hundreds of assets, keep only one version
of every asset and let WARP deal with the hassle of maintaining each platform
specific screen density variant. That is `drawable-XXX` folders in Android and
`assetName@XXX` files in iOS.

* Scaling
Don't waste time using external tools scaling assets, WARP will generate every
asset for you.

* Optimization *(or how to make you app size way smaller)*
WARP uses top notch algorithms to make your assets lightweight without any
noticeable loss of quality. You can spect a reduction in your assets total size
of at least 50%.

* Fast integration
You can safely integrate WARP into your building pipeline, WARP will skip
already processed assets. If no changes were made in your assets folder, WARP
can completely run in almost 0 seconds.

## Installation

### Dependencies
WARP uses `pngquant` to achieve astonishing good compression ratios and
`ffmpeg` to scale images in a split second. To run warp you need to install
those libraries first.

**Linux:**
```shell
sudo apt-get update
sudo apt-get -y install pngquant
sudo apt-get -y install ffmpeg
```
**MacOS** *(using Homebrew)*
```shell
brew install pngquant
brew install ffmpeg
```

### WARP
Warp is a self-contained utility, just download `warp.py` and you are good to go.

## Basic usage
A basic usage of WARP looks like this:
```shell
./warp.py --target android
```
This will generate two folders:
* `raw`: Place you original assets file here. They should be in `XXX-HDPI` for
Android and `@3X` for iOS. The other variants will be generated automatically.
* `assets`: The processed assets will be placed here.

Now, copy some assets inside the `raw` folder and run the script again. You'll
find your processed assets inside the `assets` folder.

The example above produces assets for Android. Feel free to use `--target ios` to
generate assets for that platform!

**Tip:** You can view a full list of commands with `./warp.py --help`

## Advanced usage

* Specify custom input and output directories with `--input [PATH]` and `--output [PATH]`
* Clear the output folder and process every asset again with `--clean`
* Hide the welcome message with `--silent`
* Every option has a shorthand version, so you can use `-i` instead of `--input`
or `-c` instead of `--clean` for example.

## Integration with Android Studio

WARP can be easily integrated with Android Studio using a Gradle task.

##### Installation

1. Download `warp.py`
2. Download `warp_task.gradle`
3. Place both files under `YOUR/PROJECT/PATH/scripts/warp/`
4. Place the following line in your project's `app.gradle` file:

```
apply plugin: 'com.android.application'
apply from: '../scripts/warp/warp_task.gradle' //Add this line

android {
    ...
}
```
5. Press "sync with gradle" in Android Studio
6. Place your assets in the generated `raw` folder in your project's root
directory.

That's it. Remember to run "sync with gradle" after adding new assets, this
will run WARP and generate the assets for your project.

## Benchmarks
Sample: 256 icon assets from an Android Play Store published app. The assets where
converted and optimized to HDPI, XHDPI, XXHDPI and XXXHDPI screen densities.

#### Processing
* First run processing time: 44 seconds.
* Second run (no changes) processing time: < 1 second.
* Hardware: MacBook Pro 15" 2016 (Intel i7, 16GB of RAM)

#### Compression
* Original assets size: 3,4 MB
* Size after optimization: 1,7 MB
* Total size reduction: 50%

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push your branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## About ##

This project is maintained by [Juan Ignacio Molina](https://github.com/juanignaciomolina)
and it was written by [Wolox](http://www.wolox.com.ar).

![Wolox](https://raw.githubusercontent.com/Wolox/press-kit/master/logos/logo_banner.png)

## License

**WARP** is available under the MIT [license](https://raw.githubusercontent.com/Wolox/warp/master/LICENSE.md).

    Copyright (c) 2017 Juan Ignacio Molina, aka Juani

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
