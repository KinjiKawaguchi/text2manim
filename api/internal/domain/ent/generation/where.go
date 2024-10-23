// Code generated by ent, DO NOT EDIT.

package generation

import (
	"time"

	"entgo.io/ent/dialect/sql"
	"github.com/KinjiKawaguchi/text2manim/api/internal/domain/ent/predicate"
	"github.com/google/uuid"
)

// ID filters vertices based on their ID field.
func ID(id uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldID, id))
}

// IDEQ applies the EQ predicate on the ID field.
func IDEQ(id uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldID, id))
}

// IDNEQ applies the NEQ predicate on the ID field.
func IDNEQ(id uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldID, id))
}

// IDIn applies the In predicate on the ID field.
func IDIn(ids ...uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldID, ids...))
}

// IDNotIn applies the NotIn predicate on the ID field.
func IDNotIn(ids ...uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldID, ids...))
}

// IDGT applies the GT predicate on the ID field.
func IDGT(id uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldGT(FieldID, id))
}

// IDGTE applies the GTE predicate on the ID field.
func IDGTE(id uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldGTE(FieldID, id))
}

// IDLT applies the LT predicate on the ID field.
func IDLT(id uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldLT(FieldID, id))
}

// IDLTE applies the LTE predicate on the ID field.
func IDLTE(id uuid.UUID) predicate.Generation {
	return predicate.Generation(sql.FieldLTE(FieldID, id))
}

// Prompt applies equality check predicate on the "prompt" field. It's identical to PromptEQ.
func Prompt(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldPrompt, v))
}

// VideoURL applies equality check predicate on the "video_url" field. It's identical to VideoURLEQ.
func VideoURL(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldVideoURL, v))
}

// ScriptURL applies equality check predicate on the "script_url" field. It's identical to ScriptURLEQ.
func ScriptURL(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldScriptURL, v))
}

// ErrorMessage applies equality check predicate on the "error_message" field. It's identical to ErrorMessageEQ.
func ErrorMessage(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldErrorMessage, v))
}

// UpdatedAt applies equality check predicate on the "updated_at" field. It's identical to UpdatedAtEQ.
func UpdatedAt(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldUpdatedAt, v))
}

// CreatedAt applies equality check predicate on the "created_at" field. It's identical to CreatedAtEQ.
func CreatedAt(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldCreatedAt, v))
}

// PromptEQ applies the EQ predicate on the "prompt" field.
func PromptEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldPrompt, v))
}

// PromptNEQ applies the NEQ predicate on the "prompt" field.
func PromptNEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldPrompt, v))
}

// PromptIn applies the In predicate on the "prompt" field.
func PromptIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldPrompt, vs...))
}

// PromptNotIn applies the NotIn predicate on the "prompt" field.
func PromptNotIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldPrompt, vs...))
}

// PromptGT applies the GT predicate on the "prompt" field.
func PromptGT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGT(FieldPrompt, v))
}

// PromptGTE applies the GTE predicate on the "prompt" field.
func PromptGTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGTE(FieldPrompt, v))
}

// PromptLT applies the LT predicate on the "prompt" field.
func PromptLT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLT(FieldPrompt, v))
}

// PromptLTE applies the LTE predicate on the "prompt" field.
func PromptLTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLTE(FieldPrompt, v))
}

// PromptContains applies the Contains predicate on the "prompt" field.
func PromptContains(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContains(FieldPrompt, v))
}

// PromptHasPrefix applies the HasPrefix predicate on the "prompt" field.
func PromptHasPrefix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasPrefix(FieldPrompt, v))
}

// PromptHasSuffix applies the HasSuffix predicate on the "prompt" field.
func PromptHasSuffix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasSuffix(FieldPrompt, v))
}

// PromptIsNil applies the IsNil predicate on the "prompt" field.
func PromptIsNil() predicate.Generation {
	return predicate.Generation(sql.FieldIsNull(FieldPrompt))
}

// PromptNotNil applies the NotNil predicate on the "prompt" field.
func PromptNotNil() predicate.Generation {
	return predicate.Generation(sql.FieldNotNull(FieldPrompt))
}

// PromptEqualFold applies the EqualFold predicate on the "prompt" field.
func PromptEqualFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEqualFold(FieldPrompt, v))
}

// PromptContainsFold applies the ContainsFold predicate on the "prompt" field.
func PromptContainsFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContainsFold(FieldPrompt, v))
}

// StatusEQ applies the EQ predicate on the "status" field.
func StatusEQ(v Status) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldStatus, v))
}

// StatusNEQ applies the NEQ predicate on the "status" field.
func StatusNEQ(v Status) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldStatus, v))
}

// StatusIn applies the In predicate on the "status" field.
func StatusIn(vs ...Status) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldStatus, vs...))
}

// StatusNotIn applies the NotIn predicate on the "status" field.
func StatusNotIn(vs ...Status) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldStatus, vs...))
}

// VideoURLEQ applies the EQ predicate on the "video_url" field.
func VideoURLEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldVideoURL, v))
}

// VideoURLNEQ applies the NEQ predicate on the "video_url" field.
func VideoURLNEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldVideoURL, v))
}

// VideoURLIn applies the In predicate on the "video_url" field.
func VideoURLIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldVideoURL, vs...))
}

// VideoURLNotIn applies the NotIn predicate on the "video_url" field.
func VideoURLNotIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldVideoURL, vs...))
}

// VideoURLGT applies the GT predicate on the "video_url" field.
func VideoURLGT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGT(FieldVideoURL, v))
}

// VideoURLGTE applies the GTE predicate on the "video_url" field.
func VideoURLGTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGTE(FieldVideoURL, v))
}

// VideoURLLT applies the LT predicate on the "video_url" field.
func VideoURLLT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLT(FieldVideoURL, v))
}

// VideoURLLTE applies the LTE predicate on the "video_url" field.
func VideoURLLTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLTE(FieldVideoURL, v))
}

// VideoURLContains applies the Contains predicate on the "video_url" field.
func VideoURLContains(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContains(FieldVideoURL, v))
}

// VideoURLHasPrefix applies the HasPrefix predicate on the "video_url" field.
func VideoURLHasPrefix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasPrefix(FieldVideoURL, v))
}

// VideoURLHasSuffix applies the HasSuffix predicate on the "video_url" field.
func VideoURLHasSuffix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasSuffix(FieldVideoURL, v))
}

// VideoURLIsNil applies the IsNil predicate on the "video_url" field.
func VideoURLIsNil() predicate.Generation {
	return predicate.Generation(sql.FieldIsNull(FieldVideoURL))
}

// VideoURLNotNil applies the NotNil predicate on the "video_url" field.
func VideoURLNotNil() predicate.Generation {
	return predicate.Generation(sql.FieldNotNull(FieldVideoURL))
}

// VideoURLEqualFold applies the EqualFold predicate on the "video_url" field.
func VideoURLEqualFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEqualFold(FieldVideoURL, v))
}

// VideoURLContainsFold applies the ContainsFold predicate on the "video_url" field.
func VideoURLContainsFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContainsFold(FieldVideoURL, v))
}

// ScriptURLEQ applies the EQ predicate on the "script_url" field.
func ScriptURLEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldScriptURL, v))
}

// ScriptURLNEQ applies the NEQ predicate on the "script_url" field.
func ScriptURLNEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldScriptURL, v))
}

// ScriptURLIn applies the In predicate on the "script_url" field.
func ScriptURLIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldScriptURL, vs...))
}

// ScriptURLNotIn applies the NotIn predicate on the "script_url" field.
func ScriptURLNotIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldScriptURL, vs...))
}

// ScriptURLGT applies the GT predicate on the "script_url" field.
func ScriptURLGT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGT(FieldScriptURL, v))
}

// ScriptURLGTE applies the GTE predicate on the "script_url" field.
func ScriptURLGTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGTE(FieldScriptURL, v))
}

// ScriptURLLT applies the LT predicate on the "script_url" field.
func ScriptURLLT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLT(FieldScriptURL, v))
}

// ScriptURLLTE applies the LTE predicate on the "script_url" field.
func ScriptURLLTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLTE(FieldScriptURL, v))
}

// ScriptURLContains applies the Contains predicate on the "script_url" field.
func ScriptURLContains(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContains(FieldScriptURL, v))
}

// ScriptURLHasPrefix applies the HasPrefix predicate on the "script_url" field.
func ScriptURLHasPrefix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasPrefix(FieldScriptURL, v))
}

// ScriptURLHasSuffix applies the HasSuffix predicate on the "script_url" field.
func ScriptURLHasSuffix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasSuffix(FieldScriptURL, v))
}

// ScriptURLIsNil applies the IsNil predicate on the "script_url" field.
func ScriptURLIsNil() predicate.Generation {
	return predicate.Generation(sql.FieldIsNull(FieldScriptURL))
}

// ScriptURLNotNil applies the NotNil predicate on the "script_url" field.
func ScriptURLNotNil() predicate.Generation {
	return predicate.Generation(sql.FieldNotNull(FieldScriptURL))
}

// ScriptURLEqualFold applies the EqualFold predicate on the "script_url" field.
func ScriptURLEqualFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEqualFold(FieldScriptURL, v))
}

// ScriptURLContainsFold applies the ContainsFold predicate on the "script_url" field.
func ScriptURLContainsFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContainsFold(FieldScriptURL, v))
}

// ErrorMessageEQ applies the EQ predicate on the "error_message" field.
func ErrorMessageEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldErrorMessage, v))
}

// ErrorMessageNEQ applies the NEQ predicate on the "error_message" field.
func ErrorMessageNEQ(v string) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldErrorMessage, v))
}

// ErrorMessageIn applies the In predicate on the "error_message" field.
func ErrorMessageIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldErrorMessage, vs...))
}

// ErrorMessageNotIn applies the NotIn predicate on the "error_message" field.
func ErrorMessageNotIn(vs ...string) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldErrorMessage, vs...))
}

// ErrorMessageGT applies the GT predicate on the "error_message" field.
func ErrorMessageGT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGT(FieldErrorMessage, v))
}

// ErrorMessageGTE applies the GTE predicate on the "error_message" field.
func ErrorMessageGTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldGTE(FieldErrorMessage, v))
}

// ErrorMessageLT applies the LT predicate on the "error_message" field.
func ErrorMessageLT(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLT(FieldErrorMessage, v))
}

// ErrorMessageLTE applies the LTE predicate on the "error_message" field.
func ErrorMessageLTE(v string) predicate.Generation {
	return predicate.Generation(sql.FieldLTE(FieldErrorMessage, v))
}

// ErrorMessageContains applies the Contains predicate on the "error_message" field.
func ErrorMessageContains(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContains(FieldErrorMessage, v))
}

// ErrorMessageHasPrefix applies the HasPrefix predicate on the "error_message" field.
func ErrorMessageHasPrefix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasPrefix(FieldErrorMessage, v))
}

// ErrorMessageHasSuffix applies the HasSuffix predicate on the "error_message" field.
func ErrorMessageHasSuffix(v string) predicate.Generation {
	return predicate.Generation(sql.FieldHasSuffix(FieldErrorMessage, v))
}

// ErrorMessageIsNil applies the IsNil predicate on the "error_message" field.
func ErrorMessageIsNil() predicate.Generation {
	return predicate.Generation(sql.FieldIsNull(FieldErrorMessage))
}

// ErrorMessageNotNil applies the NotNil predicate on the "error_message" field.
func ErrorMessageNotNil() predicate.Generation {
	return predicate.Generation(sql.FieldNotNull(FieldErrorMessage))
}

// ErrorMessageEqualFold applies the EqualFold predicate on the "error_message" field.
func ErrorMessageEqualFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldEqualFold(FieldErrorMessage, v))
}

// ErrorMessageContainsFold applies the ContainsFold predicate on the "error_message" field.
func ErrorMessageContainsFold(v string) predicate.Generation {
	return predicate.Generation(sql.FieldContainsFold(FieldErrorMessage, v))
}

// UpdatedAtEQ applies the EQ predicate on the "updated_at" field.
func UpdatedAtEQ(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldUpdatedAt, v))
}

// UpdatedAtNEQ applies the NEQ predicate on the "updated_at" field.
func UpdatedAtNEQ(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldUpdatedAt, v))
}

// UpdatedAtIn applies the In predicate on the "updated_at" field.
func UpdatedAtIn(vs ...time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldUpdatedAt, vs...))
}

// UpdatedAtNotIn applies the NotIn predicate on the "updated_at" field.
func UpdatedAtNotIn(vs ...time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldUpdatedAt, vs...))
}

// UpdatedAtGT applies the GT predicate on the "updated_at" field.
func UpdatedAtGT(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldGT(FieldUpdatedAt, v))
}

// UpdatedAtGTE applies the GTE predicate on the "updated_at" field.
func UpdatedAtGTE(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldGTE(FieldUpdatedAt, v))
}

// UpdatedAtLT applies the LT predicate on the "updated_at" field.
func UpdatedAtLT(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldLT(FieldUpdatedAt, v))
}

// UpdatedAtLTE applies the LTE predicate on the "updated_at" field.
func UpdatedAtLTE(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldLTE(FieldUpdatedAt, v))
}

// CreatedAtEQ applies the EQ predicate on the "created_at" field.
func CreatedAtEQ(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldEQ(FieldCreatedAt, v))
}

// CreatedAtNEQ applies the NEQ predicate on the "created_at" field.
func CreatedAtNEQ(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldNEQ(FieldCreatedAt, v))
}

// CreatedAtIn applies the In predicate on the "created_at" field.
func CreatedAtIn(vs ...time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldIn(FieldCreatedAt, vs...))
}

// CreatedAtNotIn applies the NotIn predicate on the "created_at" field.
func CreatedAtNotIn(vs ...time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldNotIn(FieldCreatedAt, vs...))
}

// CreatedAtGT applies the GT predicate on the "created_at" field.
func CreatedAtGT(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldGT(FieldCreatedAt, v))
}

// CreatedAtGTE applies the GTE predicate on the "created_at" field.
func CreatedAtGTE(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldGTE(FieldCreatedAt, v))
}

// CreatedAtLT applies the LT predicate on the "created_at" field.
func CreatedAtLT(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldLT(FieldCreatedAt, v))
}

// CreatedAtLTE applies the LTE predicate on the "created_at" field.
func CreatedAtLTE(v time.Time) predicate.Generation {
	return predicate.Generation(sql.FieldLTE(FieldCreatedAt, v))
}

// And groups predicates with the AND operator between them.
func And(predicates ...predicate.Generation) predicate.Generation {
	return predicate.Generation(sql.AndPredicates(predicates...))
}

// Or groups predicates with the OR operator between them.
func Or(predicates ...predicate.Generation) predicate.Generation {
	return predicate.Generation(sql.OrPredicates(predicates...))
}

// Not applies the not operator on the given predicate.
func Not(p predicate.Generation) predicate.Generation {
	return predicate.Generation(sql.NotPredicates(p))
}