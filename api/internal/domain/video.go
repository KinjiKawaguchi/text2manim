package domain

import (
	"time"
)

type Video struct {
	ID        string `gorm:"primaryKey"`
	Prompt    string
	Status    VideoStatus
	VideoURL  string
	UpdatedAt time.Time
	CreatedAt time.Time
}

type VideoStatus int

const (
	StatusPending VideoStatus = iota
	StatusProcessing
	StatusCompleted
	StatusFailed
)
