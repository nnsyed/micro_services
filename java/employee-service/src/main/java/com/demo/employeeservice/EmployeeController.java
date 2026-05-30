package com.demo.employeeservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/employees")
public class EmployeeController {

    @Autowired
    private EmployeeRepository repository;

    @GetMapping
    public Map<String, Object> getAllEmployees() {
        Map<String, Object> response = new HashMap<>();
        response.put("data", repository.findAll());
        return response;
    }

    @PostMapping
    public Map<String, String> createEmployee(@RequestBody Employee employee) {
        repository.save(employee);
        return Collections.singletonMap("status", "created");
    }

    @PutMapping("/{id}")
    public Map<String, String> updateEmployee(@PathVariable Long id, @RequestBody Employee employeeDetails) {
        Employee employee = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Employee not found with id: " + id));
        
        employee.setName(employeeDetails.getName());
        employee.setRole(employeeDetails.getRole());
        employee.setDepartment(employeeDetails.getDepartment());
        
        repository.save(employee);
        return Collections.singletonMap("status", "updated");
    }

    @DeleteMapping("/{id}")
    public Map<String, String> deleteEmployee(@PathVariable Long id) {
        repository.deleteById(id);
        return Collections.singletonMap("status", "deleted");
    }
}