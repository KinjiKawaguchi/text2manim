FROM golang:1.23.1 as builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /text2manim-api ./cmd/server

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /text2manim-api .
COPY config/config.yaml ./config/config.yaml
CMD ["./text2manim-api"]