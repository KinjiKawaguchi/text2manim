package schema

import (
	"time"

	"entgo.io/ent"
	"entgo.io/ent/schema/field"
	"github.com/google/uuid"
)

// Generation holds the schema definition for the Generation entity.
type Generation struct {
	ent.Schema
}

// Fields of the Generation.
func (Generation) Fields() []ent.Field {
	return []ent.Field{
		field.UUID("id", uuid.UUID{}).Default(uuid.New).Unique(),
		field.String("prompt").Optional(),
		field.Enum("status").
			Values(
				"unspecified",
				"pending",
				"processing",
				"completed",
				"failed",
			).
			Default("unspecified"),
		field.String("video_url").Optional(),
		field.String("script_url").Optional(),
		field.String("error_message").Optional().Comment("失敗理由を格納するフィールド"),
		field.Time("updated_at").Default(time.Now).UpdateDefault(time.Now),
		field.Time("created_at").Default(time.Now).Immutable(),
	}
}

// Edges of the Generation.
func (Generation) Edges() []ent.Edge {
	return nil
}
