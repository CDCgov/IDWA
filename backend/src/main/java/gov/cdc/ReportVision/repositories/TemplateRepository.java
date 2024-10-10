package gov.cdc.ReportVision.repositories;


import gov.cdc.ReportVision.models.Template;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface TemplateRepository extends JpaRepository<Template, UUID> {
}
