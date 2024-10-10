package gov.cdc.ReportVision.models;

import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import lombok.Getter;

import java.util.List;
import java.util.UUID;

@Getter
@Entity
public class Extraction extends BaseEntity {
    @Id
    @GeneratedValue(generator = "UUID4")
    @Column(updatable = false, nullable = false)
    private UUID id;

    @Enumerated(EnumType.STRING)
    private ExtractionStatus status;

    @ManyToOne
    private Template segmentationTemplate;

    @ElementCollection
    private List<String> sourceImages;

    @OneToMany(mappedBy = "extraction")
    private List<ExtractedField> fields;

    @OneToMany(mappedBy = "extraction")
    private List<ExtractedField> corrections;

    @ManyToOne
    private Upload upload;
}
