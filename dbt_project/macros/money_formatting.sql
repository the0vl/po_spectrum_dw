{% macro format_money(column_name) %}
    ROUND({{ column_name }}, 2)
{% endmacro %}