<!-- Package: 00_skills/(development)/shopify-developer; relative command/resource examples resolve from that package or workspace root. -->

## Liquid Essentials

Three syntax types:

```liquid
{{ product.title | upcase }}                    {# Output with filter #}
{% if product.available %}In stock{% endif %}   {# Logic tag #}
{% assign sale = product.price | times: 0.8 %}  {# Assignment #}
{%- if condition -%}Stripped whitespace{%- endif -%}
```

Key patterns:

```liquid
{% for product in collection.products limit: 5 %}
  {% render 'product-card', product: product %}
{% endfor %}

{% paginate collection.products by 12 %}
  {% for product in paginate.collection.products %}...{% endfor %}
  {{ paginate | default_pagination }}
{% endpaginate %}
```
