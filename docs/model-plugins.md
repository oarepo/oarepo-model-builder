
  processing-order: [ 'settings', '*', 'model' ]


  plugins:
    packages: [ ]
    # list of extra packages that should be installed in compiler's venv
    output|builder|model|property:
      # plugin types - file outputs, builders, model preprocessors, property preprocessors 
      disabled: [ ]
      # list of plugin names to disable
      # string "__all__" to disable all plugins in this category    
      enabled:
      # list of plugin names to enable. The plugins will be used
      # in the order defined. Use with disabled: __all__
      # list of "module:className" that will be added at the end of
      # plugin list