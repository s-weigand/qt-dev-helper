{{ objname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block attributes_summary %}
    {% if all_attributes %}

    .. rubric:: Attributes Summary

    .. autosummary::
    {% for item in all_attributes %}
        ~{{ item }}
    {%- endfor %}

    {% endif %}
    {% endblock %}

    {% block methods_summary %}
    {% if all_methods %}

     {% if '__init__' in methods %}
        {% set caught_result = methods.remove('__init__') %}
    {% endif %}

    .. rubric:: Methods Summary

    .. autosummary::
        :toctree: {{ objname }}/methods
        :nosignatures:

    {% for item in all_methods %}
        ~{{ name }}.{{ item }}
    {%- endfor %}

    {% endif %}
    {% endblock %}

    {% block methods_documentation %}
    {% if methods %}

    .. rubric:: Methods Documentation

    {% for item in all_methods %}
    .. automethod:: {{ name }}.{{ item }}
    {%- endfor %}

    {% endif %}
    {% endblock %}
