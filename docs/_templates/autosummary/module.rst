{% block module %}
{{ name  | escape | underline }}

.. currentmodule:: {{ module }}

.. automodule:: {{ fullname }}


{% block modules %}
  {% if all_modules %}

  .. rubric:: Modules

  .. autosummary::
    :toctree: {{ name }}
    :recursive:

    {% for item in all_modules %}
      {{ item }}
    {%- endfor %}

  {% endif %}

{% endblock %}


{% block attributes %}
  {% if all_attributes %}
  .. rubric:: Module Attributes

  .. autosummary::
      :toctree: {{ name }}

      {% for item in all_attributes %}
          {{ item }}
      {%- endfor %}

  {% endif %}

{% endblock %}

{% block functions %}
  {% if all_functions %}

Functions
---------

  .. rubric:: Summary

  .. autosummary::
      :toctree: {{ name }}/functions
      :nosignatures:

      {% for item in all_functions %}
        {{ item }}
      {%- endfor %}

  {% endif %}

{% endblock %}

{% block classes %}
  {% if all_classes %}

Classes
-------

  .. rubric:: Summary

  .. autosummary::
      :toctree: {{ name }}/classes
      :nosignatures:

      {% for item in all_classes %}
        {{ item }}
      {%- endfor %}

  {% endif %}

{% endblock %}


{% block exceptions %}
  {% if all_exceptions %}

Exceptions
----------

  .. rubric:: Exception Summary

  .. autosummary::
      :toctree: {{ name }}/exceptions
      :nosignatures:

      {% for item in all_exceptions %}
          {{ item }}
      {%- endfor %}

  {% endif %}

{% endblock %}


{% endblock %}
