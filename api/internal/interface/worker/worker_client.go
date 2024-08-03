package worker

import (
	"context"
)

type WorkerClient interface {
	GenerateManimScript(ctx context.Context, taskID, prompt string) (string, error)
	GenerateManimVideo(ctx context.Context, taskID, script string) (string, error)
}
