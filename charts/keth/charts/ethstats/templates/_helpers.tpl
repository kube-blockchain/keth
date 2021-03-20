{{/* vim: set filetype=mustache: */}}

{{/* Helm required labels */}}
{{- define "ethstats.labels" -}}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/name: {{ template "ethstats.name" . }}
helm.sh/chart: {{ template "ethstats.chart" . }}
{{- if .Values.podLabels }}
{{ .Values.podLabels | toYaml }}
{{- end }}
{{- end -}}

{{/*
Expand the name of the chart.
*/}}
{{- define "ethstats.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "ethstats.fullname" -}}
{{- if .Values.overrides.fullName -}}
{{- .Values.overrides.fullName | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.overrides.name -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-keth-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ethstats.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "ethstats.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "ethstats.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return the name of the Secret used to store credentials
*/}}
{{- define "ethstats.secretName" -}}
{{- if .Values.credentials.secretName }}
{{- .Values.credentials.secretName }}
{{- else -}}
{{- template "ethstats.fullname" . }}
{{- end -}}
{{- end -}}
