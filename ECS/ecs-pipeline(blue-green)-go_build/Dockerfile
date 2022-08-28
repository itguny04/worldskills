# Build
FROM golang:latest AS builder

WORKDIR /buildspace

COPY app.go .
RUN CGO_ENABLED=0 GOOS=linux 
RUN go build -o app app.go

# Run
FROM alpine:latest AS runtime

RUN apk add libc6-compat

WORKDIR /opt/app

COPY --from=builder /buildspace/app .
COPY static static

CMD ["./app"]
EXPOSE 8080
