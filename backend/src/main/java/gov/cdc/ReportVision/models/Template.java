package gov.cdc.ReportVision.models;


import jakarta.persistence.Column;
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

@Entity
@Getter
public class Template extends BaseEntity {

  @Id
  @GeneratedValue(generator = "UUID4")
  @Column(updatable = false, nullable = false)
  private UUID id;


  private String name;
  private String description;
  private String labName;

  @OneToMany(mappedBy = "template")
  private List<Page> pages;

  @Enumerated(EnumType.STRING)
  private TemplateStatus status;

  @ManyToOne
  private Organization organization;
}


