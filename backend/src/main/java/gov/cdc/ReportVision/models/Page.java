package gov.cdc.ReportVision.models;

import jakarta.persistence.*;
import lombok.Getter;

import java.util.List;
import java.util.UUID;

@Getter
@Entity
public class Page extends BaseEntity {
    @Id
    @GeneratedValue(generator = "UUID4")
    @Column(updatable = false, nullable = false)
    private UUID id;


    @JoinTable(
        name = "page_labels",
        joinColumns = @JoinColumn(name = "page_id"),
        inverseJoinColumns = @JoinColumn(name = "label_id"))
    @OneToMany
    private List<Label> labels;

    //base64 image
    private String sourceImage;
    //base 64 image
    private String templateImage;
    //json array
    private String shapes;

    @ManyToOne(fetch = FetchType.LAZY)
    private Template template;
}