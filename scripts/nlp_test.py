import matplotlib as mpl
print(mpl.__version__)
print(mpl.matplotlib_fname())
mpl.font_manager._rebuild()

print(cudf.Series([1, 2, 3]))
# mpl.get_cachedir()
# fonts = set([f.name for f in matplotlib.font_manager.fontManager.ttflist])
# print(fonts)
# fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
# print(fonts)
