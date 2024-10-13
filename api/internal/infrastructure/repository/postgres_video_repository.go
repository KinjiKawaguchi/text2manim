// internal/infrastructure/repository/postgres_video_repository.go
package repository

import (
	"context"
	"fmt"
	"log/slog"

	"github.com/KinjiKawaguchi/text2manim/api/internal/config"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type PostgresVideoRepository struct {
	db     *gorm.DB
	logger *slog.Logger
}

func NewPostgresVideoRepository(cfg *config.Config, logger *slog.Logger) (*PostgresVideoRepository, error) {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=require",
		cfg.DBHost, cfg.DBUser, cfg.DBPassword, cfg.DBName, cfg.DBPort)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, err
	}

	// Auto Migrate
	err = db.AutoMigrate(&domain.Video{})
	if err != nil {
		return nil, err
	}

	return &PostgresVideoRepository{db: db, logger: logger}, nil
}

func (r *PostgresVideoRepository) FindByID(ctx context.Context, id string) (*domain.Video, error) {
	var video domain.Video
	result := r.db.First(&video, "id = ?", id)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, result.Error
	}
	return &video, nil
}

func (r *PostgresVideoRepository) Save(ctx context.Context, video *domain.Video) error {
	result := r.db.Create(video)
	return result.Error
}

func (r *PostgresVideoRepository) Update(ctx context.Context, video *domain.Video) error {
	result := r.db.Save(video)
	return result.Error
}

func (r *PostgresVideoRepository) Close() error {
	sqlDB, err := r.db.DB()
	if err != nil {
		return err
	}
	return sqlDB.Close()
}
