package gov.cdc.ReportVision.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.OneToMany;
import lombok.Getter;

import java.util.List;
import java.util.UUID;

@Getter
@Entity
public class Organization extends BaseEntity {
    @Id
    @GeneratedValue(generator = "UUID4")
    @Column(updatable = false, nullable = false)
    private UUID id;

    private String name;

    @JoinTable(
        name = "organization_admins",
        joinColumns = @JoinColumn(name = "organization_id"),
        inverseJoinColumns = @JoinColumn(name = "api_user_id"))
    @OneToMany
    private List<ApiUser> admins;
}