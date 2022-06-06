```
               __         _    __
 ___ ____  ___/ /______  (_)__/ /
/ _ `/ _ \/ _  / __/ _ \/ / _  /
\_,_/_//_/\_,_/_/  \___/_/\_,_/
               resource cleanup
```

## Introduction

### Motivation

Android Studio has a built in option for removing unused resources. Unfortunately, it has some [bugs][1]. In trying to find an alternative, I found [android-resource-cleaner][2] which does what I wanted. Unfortunately, it hasn't been updated in a fewa years, and considering that Python 2 is now deprecated and no longer comes install on OS X, I made my own version based on the aforementioned project.

### Changes from android-resource-cleaner

* support for Python 3
* use [ripgrep][3] instead of `grep`.
* use [xmlstarlet][4] instead of `sed` to not break json in edge cases.
* added a script for removing unused colors.
* support for webp in drawable cleanup.
* added support for ignoring lint baselines.

### How it Works

All these scripts work in pretty much the same way - given a list of files or a folder, they search for resource references (by means of @[resourceType] or R.resourceType references) for the resource. If not found, the resource is removed.

### Limitations

There are some important limitations:

* dynamically loaded resources (i.e. looking them up by name at runtime via `getIdentifier`, etc) will likely be detected as "unused" even if they are used. This is because there's no easy way to figure out that they're in use, since they're not actually referencing an `R` type directly, and instead, the resource name is constructed from a string at runtime.
* resource references looking like `layout.foo` (where the `import` statement imports `R.layout` instead of `R`) may be detected as unused, despite being in use. This is not difficult to work around, however.


## Usage

### Tools Needed

* Python 3 - no extra modules or packages necessary.
* [ripgrep][3] - it's very fast and has some nice features over grep. on macOS, `brew install ripgrep`.
* [fd][5] - a really nice faster find tool. on macOS, `brew install fd`.
* [xmlstarlet][4] - this is for properly updating xml without breaking it. on  macOS, `brew install xmlstarlet`.

### How to Run

Most of these are run in the same way - use something like `fd` to find each file of the corresponding type (for `colors`, `dimens`, and `strings`) and pass them in to their corresponding scripts. For `drawable` and `layout` resources, the directories are passed in instead.

#### Layouts

Pass the set of `layout` directories to `clean_layouts` script, one by one:

```sh
for i in `fd -p 'src/main/res/layout' -td`; do
  python3 clean_layouts.py $i/
done
```

### Drawables

Pass the set of `res` directories to `clean_drawable` script, one by one:

```sh
for i in `fd res -td | rg src/main/res`; do
  python3 clean_drawable.py $i/
done
```

### Strings

Pass each main `strings.xml` to the `clean_strings` script. It will take care of removing the corresponding language translations for any strings it removes.

```sh
for i in `fd -p 'main/res/values/strings.xml'`; do
  python3 clean_strings.py $i
done
```


### Dimension

Pass each `dimens.xml` file to `clean_dimens` script, one by one.

```sh
for i in `fd dimens.xml`; do
  python3 clean_dimens.py $i
done
```

### Colors

Pass each `colors.xml` to `clean_colors` script, one by one.

```sh
for i in `fd colors.xml`; do
  python3 clean_colors.py $i
done
```

[1]: https://issuetracker.google.com/issues/141578652
[2]: https://github.com/oxsoft/android-resource-cleaner
[3]: https://github.com/BurntSushi/ripgrep
[4]: http://xmlstar.sourceforge.net
[5]: https://github.com/sharkdp/fd
