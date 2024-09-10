{{- define "deployment.template" }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{.service.name}}
  labels:
    app.kubernetes.io/name: {{.service.name}}
    app.kubernetes.io/version: "{{ .ctx.Values.version }}"
    app.kubernetes.io/component: database
    app.kubernetes.io/part-of: simple-backend
    app.kubernetes.io/managed-by: helm
spec:
  replicas: {{.service.replicaCount}}
  selector:
    matchLabels:
      app: {{.service.name}}
  template:
    metadata:
      name: {{.service.name}}
      labels:
        app: {{.service.name}}
        app.kubernetes.io/name: {{.service.name}}
        app.kubernetes.io/version: "{{ .ctx.Values.version }}"
        app.kubernetes.io/component: database
        app.kubernetes.io/part-of: simple-backend
        app.kubernetes.io/managed-by: helm
    spec:
      containers:
        - name: {{.service.name}}
          image: library/postgres:{{ .ctx.Values.version }}-alpine
          imagePullPolicy: Always
          env:
            - name: POSTGRES_USER
              value: {{ .ctx.Values.default_database.user }}
            - name: POSTGRES_PASSWORD
              value: {{ .ctx.Values.default_database.password }}
            - name: POSTGRES_DB
              value: {{ .service.name }}
          resources:
            requests:
              memory: "{{ .ctx.Values.resources.requests.memory }}"
              cpu: "{{ .ctx.Values.resources.requests.cpu }}"
            limits:
              memory: "{{ .ctx.Values.resources.limits.memory }}"
              cpu: "{{ .ctx.Values.resources.limits.cpu }}"
          ports:
            - name: {{.service.name}}
              containerPort: {{ .ctx.Values.port }}
              hostPort: {{ .service.hostPort }}
          volumeMounts:
            - name: db-{{.service.name}}
              mountPath: /var/lib/postgresql/data
            - name: postgres-config-map
              mountPath: /docker-entrypoint-initdb.d/
              command: ["psql", "-U", "{{ .ctx.Values.default_database.user }}", "-d", "{{ .service.name }}", "-f", "/docker-entrypoint-initdb.d/init-db.sql"]
      volumes:
        - name: db-{{.service.name}}
        - name: postgres-config-map
          configMap:
            name: {{ .ctx.Release.Name }}-configmap-{{ .service.name }}
{{- end}}