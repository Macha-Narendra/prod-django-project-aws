{{- define "django-app.name" -}}
{{- default .Chart.Name .Chart.Name -}}
{{- end -}}

{{- define "django-app.fullname" -}}
{{- printf "%s-%s" (include "django-app.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
