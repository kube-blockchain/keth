{{/* vim: set filetype=mustache: */}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "geth.fullname" -}}
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

{{/* Helm required labels */}}
{{- define "geth.labels" -}}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/name: {{ template "geth.name" . }}
helm.sh/chart: {{ template "geth.chart" . }}
{{- if .Values.podLabels }}
{{ .Values.podLabels | toYaml }}
{{- end }}
{{- end -}}

{{/*
Expand the name of the chart.
*/}}
{{- define "geth.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "geth.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "geth.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{ default (include "geth.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
{{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return the name of the Secret used to store credentials
*/}}
{{- define "geth.secretName" -}}
{{- if .Values.account.secretName }}
{{- .Values.account.secretName }}
{{- else -}}
{{- template "geth.fullname" . }}
{{- end -}}
{{- end -}}

{{/*
Return the name of the Secret used to store ethstats secrets
*/}}
{{- define "geth.ethstatsSecretName" -}}
{{- if .Values.ethstats.secretName }}
{{- .Values.ethstats.secretName }}
{{- else -}}
{{- printf "%s-keth-ethstats" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/*
Return the name of the Service for bootnode
*/}}
{{- define "geth.bootnodeServiceName" -}}
{{- printf "%s-keth-bootnode" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Return the name of the Service for ethstats
*/}}
{{- define "geth.ethstatsServiceName" -}}
{{- printf "%s-keth-ethstats" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
