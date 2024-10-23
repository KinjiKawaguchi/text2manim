package repository

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log/slog"

	"entgo.io/ent/dialect"
	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent/generation"
	"github.com/google/uuid"

	_ "github.com/lib/pq"
)

type PostgresVideoRepository struct {
	entClient *ent.Client
	logger    *slog.Logger
}

func NewPostgresVideoRepository(cfg *config.Config, logger *slog.Logger) (*PostgresVideoRepository, error) {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=require",
		cfg.DBHost, cfg.DBUser, cfg.DBPassword, cfg.DBName, cfg.DBPort)

	entClient, err := ent.Open(dialect.Postgres, dsn)
	if err != nil {
		logger.Error("Failed to connect to database", "error", err)
		return nil, err
	}

	if err := entClient.Schema.Create(context.Background()); err != nil {
		logger.Error("Failed to create schema", "error", err)
		return nil, err
	}

	return &PostgresVideoRepository{entClient: entClient, logger: logger}, nil
}

func (r *PostgresVideoRepository) FindByID(ctx context.Context, id uuid.UUID) (*ent.Generation, error) {
	video, err := r.entClient.Generation.Query().
		Where(generation.ID(id)).
		Only(ctx)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil // TODO: ここチェック
		}
		r.logger.Error("Failed to find video by ID", "id", id, "error", err)
		return nil, err
	}

	return video, nil
}

func (r *PostgresVideoRepository) Save(ctx context.Context, video *ent.Generation) (*ent.Generation, error) {
	result, err := r.entClient.Generation.Create().
		SetID(video.ID).
		SetPrompt(video.Prompt).
		SetStatus(video.Status).
		SetVideoURL(video.VideoURL).
		SetScriptURL(video.ScriptURL).
		SetErrorMessage(video.ErrorMessage).
		SetCreatedAt(video.CreatedAt).
		SetUpdatedAt(video.UpdatedAt).
		Save(ctx)
	if err != nil {
		r.logger.Error("Failed to save video", "error", err)
		return nil, err
	}
	return result, nil
}

func (r *PostgresVideoRepository) Update(ctx context.Context, video *ent.Generation) (*ent.Generation, error) {
	result, err := r.entClient.Generation.UpdateOneID(video.ID).
		SetPrompt(video.Prompt).
		SetStatus(video.Status).
		SetVideoURL(video.VideoURL).
		SetScriptURL(video.ScriptURL).
		SetErrorMessage(video.ErrorMessage).
		SetUpdatedAt(video.UpdatedAt).
		Save(ctx)
	if err != nil {
		r.logger.Error("Failed to update video", "error", err)
		return nil, err
	}
	return result, nil
}
