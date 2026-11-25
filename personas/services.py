from config.crud import CRUDService

from .models import (
    Administrador,
    EmpresaVigilancia,
    GuardiaSeguridad,
    Persona,
    PersonaCorreo,
    PersonaTelefono,
    Residente,
    Rol,
)


class RolService(CRUDService):
    modelo = Rol

    @staticmethod
    def listar():
        return Rol.objects.all().order_by("id_rol")

    @staticmethod
    def obtener(pk):
        return Rol.objects.filter(pk=pk).first()


class EmpresaVigilanciaService(CRUDService):
    modelo = EmpresaVigilancia

    @staticmethod
    def listar():
        return EmpresaVigilancia.objects.all().order_by("nit")

    @staticmethod
    def obtener(pk):
        return EmpresaVigilancia.objects.filter(pk=pk).first()


class PersonaService(CRUDService):
    modelo = Persona

    @staticmethod
    def listar():
        return Persona.objects.select_related("id_rol", "nit_empresa").order_by("num_documento")

    @staticmethod
    def obtener(pk):
        return Persona.objects.filter(pk=pk).first()

    @staticmethod
    def listar_por_rol(id_rol):
        return Persona.objects.filter(id_rol_id=id_rol).order_by("num_documento")

    @staticmethod
    def listar_por_empresa(nit):
        return Persona.objects.filter(nit_empresa_id=nit).order_by("num_documento")


class PersonaTelefonoService(CRUDService):
    modelo = PersonaTelefono

    @staticmethod
    def listar():
        return PersonaTelefono.objects.select_related("doc_persona").order_by("doc_persona", "telefono")

    @staticmethod
    def obtener(pk, telefono=None):
        consulta = PersonaTelefono.objects.filter(doc_persona_id=pk)
        if telefono:
            consulta = consulta.filter(telefono=telefono)
        return consulta.first()

    @staticmethod
    def listar_por_persona(doc_persona):
        return PersonaTelefono.objects.filter(doc_persona_id=doc_persona).order_by("telefono")


class PersonaCorreoService(CRUDService):
    modelo = PersonaCorreo

    @staticmethod
    def listar():
        return PersonaCorreo.objects.select_related("doc_persona").order_by("doc_persona", "email")

    @staticmethod
    def obtener(pk, email=None):
        consulta = PersonaCorreo.objects.filter(doc_persona_id=pk)
        if email:
            consulta = consulta.filter(email=email)
        return consulta.first()

    @staticmethod
    def listar_por_persona(doc_persona):
        return PersonaCorreo.objects.filter(doc_persona_id=doc_persona).order_by("email")


class AdministradorService(CRUDService):
    modelo = Administrador

    @staticmethod
    def listar():
        return Administrador.objects.select_related("numero_documento").order_by("numero_documento")

    @staticmethod
    def obtener(pk):
        return Administrador.objects.filter(pk=pk).first()


class GuardiaSeguridadService(CRUDService):
    modelo = GuardiaSeguridad

    @staticmethod
    def listar():
        return GuardiaSeguridad.objects.select_related("numero_documento").order_by("numero_documento")

    @staticmethod
    def obtener(pk):
        return GuardiaSeguridad.objects.filter(pk=pk).first()


class ResidenteService(CRUDService):
    modelo = Residente

    @staticmethod
    def listar():
        return Residente.objects.select_related("numero_documento").order_by("numero_documento")

    @staticmethod
    def obtener(pk):
        return Residente.objects.filter(pk=pk).first()
