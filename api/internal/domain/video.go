package domain

import "time"

type Video struct {
	ID        string
	Prompt    string
	Status    VideoStatus
	VideoURL  string
	UpdatedAt time.Time
}

type VideoStatus int

const (
	StatusPending VideoStatus = iota
	StatusProcessing
	StatusCompleted
	StatusFailed
)
