# Мониторинг контейнеризированного приложения

## Обзор
Этот тестовый проект показывает , как развернуть приложение на Flask и настроить мониторинг Flask веб-приложения с использованием Grafana и Prometheus. Включены предварительно настроенные дашборды и правила оповещений.

## Возможности
- **Prometheus** для сбора метрик и оповещений.
- **Grafana** для визуализации данных и дашбордов.
- Docker-контейнеры для простой установки.


```

## Требования
- Установленные Docker и Docker Compose.
- Зависимости я уже включил в Dockerfile самого приложение так что не нужно устанавливать Flask , python я взял python3.12 Slim

## Шаги развертывания

### 1. Клонирование репозитория
```bash
git clone <repository_url>
cd WN-test
docker-compose up -d
```


### 2. Доступ к сервисам
- Flask веб-приложение: [http://localhost:5000](http://localhost:5000/health)
- вернет {"status":"healthy"}
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)
  - Логин: `admin`
  - Пароль: `admin`
  - После ввода задать свой пароль 


## Конфигурационные файлы

### Flask приложение
`app.py` код имеет API GET '/metrics' проверить можно c помощью http://localhost:5000/metrics
и так же еще одно API GET '/health' проверить можно с помощью http://localhost:5000/helth
или же с помощью curl 

### Конфигурация Prometheus
`prometheus.yml`:
```yaml
global:
  scrape_interval: 5s

rule_files:
  - /etc/prometheus/alert.rules

scrape_configs:
  - job_name: 'web_app'
    static_configs:
      - targets: ['web_app:5000']

```

### Правила оповещений

Реализовывал алертинг в прометеус но не делал алерт менеджер на почту или в чат так как этоо тестовое 
`alert.rules`:
```yaml
groups:
- name: web_app_alerts
  rules:
  - alert: HighResponseTime
    expr: avg(avg_response_time) > 0.5
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "Высокое время ответа"
  - alert: AppUnavailable
    expr: up{job="web_app"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Приложение недоступно"

```
для проверки алертинга достаточно прейти http://localhost:9090/alerts 
и выполнить "docker-compose stop web_app"  увидим что приложение не доступно и prometeus нам об этом сообщает firing для того что бы все снова стало хорошо 
выполните "docker-compose start web_app"
для того что бы проверить как отрабатыват Высокое время ответа "for i in {1..10000}; do curl -s http://localhost:5000/health & done" выполнить в терминале 
Можно добавить в код задержку или другими утилитами на пример 
"siege -c50 -t1M http://localhost:5000/metrics"



### Конфигурация Grafana

#### Источник данных
`datasource.yml`:
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    uid: prometheus_ds
    url: http://prometheus:9090
    access: proxy
    isDefault: true

```

#### Docker-compose.yml 
имеет единую сеть my_networks также были настроены voluems для сохранения состояний что бы при перезапусках не приходилось настраивать все заново включаяя дашборды они описанны `grafana/dashboards/dashboard.json` , он содержит предварительно настроенные панели, включая состояние приложения, среднее время ответа и количество запросов. 


## Остановка сервисов
Для остановки всех сервисов выполните:
```bash
docker-compose down
```



