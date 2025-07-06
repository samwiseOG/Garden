-- Table: public.recordId

-- DROP TABLE IF EXISTS public."recordId";

CREATE TABLE IF NOT EXISTS public."recordId"
(
    "RecordId" integer NOT NULL DEFAULT nextval('"recordId_RecordId_seq"'::regclass),
    "StartTimestamp" timestamp with time zone NOT NULL,
    "EndTimestamp" timestamp with time zone NOT NULL,
    "SensorId" character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "AvgValue" numeric NOT NULL,
    "MaxValue" numeric NOT NULL,
    "MinValue" numeric NOT NULL,
    "StandardDev" numeric NOT NULL,
    "Unit" character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "ValueCount" bigint NOT NULL,
    CONSTRAINT "recordId_pkey" PRIMARY KEY ("RecordId")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."recordId"
    OWNER to postgres;