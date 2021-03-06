# Elasticsearch settings

```yaml
settings:
  elasticsearch:
    keyword-ignore-above: 50
    templates:
      v7:
        # the default value is empty, this is just an example 
        analysis:
          analyzer:
            lower_whitespace:
              filter:
              - lowercase
              tokenizer: comma_whitespace
          tokenizer:
            comma_whitespace:
              pattern: '[ ,]'
              type: simple_pattern_split,
        mappings:
          properties:
    # version which should be generated. Only v7 is supported
    version: v7
```

Later on, in model use the defined analyzer as:

```yaml
model:
  properties:
    a:
      type: string
      oarepo:mapping:
        type: text
        analyzer: lower_whitespace
```

*Note:* everything that you put into `oarepo:mapping` section will be copied into the generated
mapping file.