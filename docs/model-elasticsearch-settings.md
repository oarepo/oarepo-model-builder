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
            # TODO: should be moved to included invenio model, not a global template
            $schema:
              type: keyword
            created:
              type: date
            id:
              type: keyword
            pid:
              properties:
                obj_type:
                  type: keyword
                pid_type:
                  type: keyword
                pk:
                  type: integer
                status:
                  type: keyword
              type: object
            updated:
              type: date
            uuid:
              type: keyword
    # version which should be generated. Only v7 is supported
    version: v7
```
