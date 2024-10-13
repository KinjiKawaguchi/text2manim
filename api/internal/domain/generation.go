package domain

import (
	"time"
)

type Generation struct {
	ID           string `gorm:"primaryKey"`
	Prompt       string
	Status       GenerationStatus
	VideoURL     string
	ScriptURL    string
	ErrorMessage string // 失敗理由を格納するフィールドを追加
	UpdatedAt    time.Time
	CreatedAt    time.Time
}

type GenerationStatus int

const (
	StatusPending GenerationStatus = iota
	StatusProcessing
	StatusCompleted
	StatusFailed
)
