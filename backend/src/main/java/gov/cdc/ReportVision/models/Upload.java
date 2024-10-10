package gov.cdc.ReportVision.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import lombok.Getter;

import java.util.Set;
import java.util.UUID;

@Getter
@Entity
public class Upload extends BaseEntity {
    @Id
    @GeneratedValue(generator = "UUID4")
    @Column(updatable = false, nullable = false)
    private UUID id;

    @ManyToOne
    private ApiUser createdBy;

    @ManyToOne
    private ApiUser updatedBy;

    @OneToMany(mappedBy = "upload")
    private Set<Extraction> extractions;
}